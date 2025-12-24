import os
import sounddevice as sd
import numpy as np
import whisper
import soundfile as sf


DEFAULT_DEVICE = int(os.getenv("AUDIO_DEVICE_INDEX", "15"))
MODEL_NAME = os.getenv("WHISPER_MODEL", "medium")

model = whisper.load_model(MODEL_NAME)


def list_input_devices():
    print(sd.query_devices())


def listen_once_gu(duration=10, samplerate=16000, device=DEFAULT_DEVICE, save_debug_wav=True):
   
   
    try:
        devices = sd.query_devices()
    except Exception:
        devices = []

    chosen = None
    if device is not None:
        try:
            
            didx = int(device)
            if 0 <= didx < len(devices) and devices[didx]["max_input_channels"] > 0:
                chosen = didx
        except Exception:
            # try matching by name
            for idx, dev in enumerate(devices):
                if str(device).lower() in dev["name"].lower() and dev["max_input_channels"] > 0:
                    chosen = idx
                    break

    if chosen is None:
        # pick DEFAULT_DEVICE if valid, else first input-capable device
        try:
            default_idx = int(DEFAULT_DEVICE)
        except Exception:
            default_idx = None
        if default_idx is not None and 0 <= default_idx < len(devices) and devices[default_idx]["max_input_channels"] > 0:
            chosen = default_idx
        else:
            for idx, dev in enumerate(devices):
                if dev["max_input_channels"] > 0:
                    chosen = idx
                    break

    if chosen is not None:
        print(f"Preferred audio input device {chosen}: {sd.query_devices(chosen)['name']}")
    else:
        print("Warning: no suitable input audio device found; recording may fail.")

    # Try to record using the chosen device; if it fails, try a few other input-capable devices.
    candidates = []
    if chosen is not None:
        candidates.append(chosen)
    for idx, dev in enumerate(devices):
        if dev.get("max_input_channels", 0) > 0 and idx not in candidates:
            candidates.append(idx)

    audio = None
    last_err = None
    for didx in candidates:
        try:
            sd.default.device = didx
            devinfo = sd.query_devices(didx)
            print(f"Trying device {didx}: {devinfo['name']} (in={devinfo['max_input_channels']})")
            # Use device's available channels (cap at 2) then convert to mono
            chan = min(2, int(devinfo.get("max_input_channels", 1)))
            audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=chan, dtype="float32")
            sd.wait()
            break
        except Exception as e:
            print(f"Device {didx} failed: {e}")
            last_err = e

    if audio is None:
        raise RuntimeError("Unable to open any input audio device. Run list_input_devices() to inspect devices.") from last_err

    # Convert to mono if multi-channel
    audio = np.asarray(audio)
    if audio.ndim > 1 and audio.shape[1] > 1:
        audio = np.mean(audio, axis=1)
    audio = np.squeeze(audio)
    if save_debug_wav:
        try:
            sf.write("input.wav", audio, samplerate)
        except Exception:
            pass

    try:
        result = model.transcribe(audio, language="gu")
    except Exception:
        sf.write("input.wav", audio, samplerate)
        result = model.transcribe("input.wav", language="gu")

    text = result.get("text", "").strip()
    print(f"Transcribed: {text}")
    return text


if __name__ == "__main__":
    print(f"Using model: {MODEL_NAME}, default device: {DEFAULT_DEVICE}")
    list_input_devices()
    listen_once_gu()