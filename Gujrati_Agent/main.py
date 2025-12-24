from agent.state_machine import State
from agent.planner import Planner
from agent.executor import Executor
from agent.evaluator import Evaluator
from agent.memory import Memory
from voice.stt import listen_once_gu
from voice.tts import speak_gu

def run():
    memory = Memory()
    planner = Planner()
    executor = Executor()
    evaluator = Evaluator()

    state = State.INIT
    speak_gu("નમસ્તે! હું ગુજરાતીમાં સરકારની યોજનાઓ માટે તમારી સહાય માટે તૈયાર છું.")

    while state != State.END:
        input('Press Enter to speak...')
        try:
            user_text = listen_once_gu()
        except Exception as e:
            speak_gu("માઇક્રોફોન સંબંધિત ત્રુટિ થઈ. કૃપા કરીને માઇક ચેક કરો અને ફરી પ્રયત્ન કરો.")
            print(f"STT error: {e}")
            continue
        if not user_text:
            speak_gu("માફ કરશો, ધ્યાનમાં શો સાબિત થયું નહીં. ફરીથી બોલો.")
            continue
        memory.remember_turn(user_text=user_text)



        text = user_text.lower()
        if "ઉંમર" in text:
            memory.update_profile("age", 28)
        if "આવક" in text or "માસિક" in text:
            memory.update_profile("income_monthly", 15000)
        if "ગાંધીનગર" in text or "જીલ્લો" in text:
            memory.update_profile("district", "Gandhinagar")
        if "ખેડૂત" in text:
            memory.update_profile("occupation", "farmer")
            memory.update_profile("farmer", True)
        if "વિદ્યાર્થી" in text:
            memory.update_profile("student", True)

        next_state, agent_msg = planner.decide(memory, user_text, state)
        speak_gu(agent_msg)
        state = next_state

        if state == State.RETRIEVE_SCHEMES:
            schemes = executor.retrieve(query=user_text, profile=memory.profile)
            if not schemes:
                speak_gu("કોઈ યોજના મળી નથી. વધુ માહિતી આપશો અથવા અલગ ક્ષેત્ર કહેશો?")
                state = State.RESOLVE_GAPS
                continue

            titles = ", ".join([s["title"] for s in schemes])
            memory.remember_turn(agent_text=f"યોજનાઓ મળી: {titles}")
            speak_gu(f"યોજનાઓ મળી: {titles}. હવે પાત્રતા તપાસું છું.")
            eligibility = executor.check(memory.profile, schemes)

            state, missing_fields = evaluator.evaluate_tools(memory, eligibility)
            if state == State.RESOLVE_GAPS:
                speak_gu(f"આ માહિતી જરૂરી છે: {', '.join(missing_fields)}.")
                continue

            eligible_list = [e for e in eligibility if e["result"]["eligible"]]
            if eligible_list:
                chosen = eligible_list[0]
                memory.chosen_scheme = chosen["scheme"]
                speak_gu(f"ભલામણ: {chosen['scheme']['title']}. અરજી કરવી છે?")
                state = State.SELECT_SCHEME
            else:
                speak_gu("હાલ કોઈ સ્પષ્ટ પાત્ર યોજના નથી. કૃપા કરીને વધુ વિગતો આપશો?")
                state = State.RESOLVE_GAPS

        if state == State.SELECT_SCHEME:
            if "હા" in text or "apply" in text or "અરજી" in text:
                state = State.APPLY
                speak_gu("હવે અરજી કરવાની પ્રક્રિયા શરૂ કરું છું.")
            else:
                speak_gu("જો તમે અરજી કરવા તૈયાર હો, તો કહો: 'અરજી કરવી છે'.")
                state = State.SELECT_SCHEME

        if state == State.APPLY:
            scheme_id = (memory.chosen_scheme or {"id": "SCHEME-001"})["id"]
            documents = executor.get_documents_for_scheme(scheme_id)
            resp = executor.apply(scheme_id=scheme_id, profile=memory.profile, documents=documents)
            if not resp["ok"]:
                speak_gu(f"અરજીમાં સમસ્યા: {resp['error']}. ફરી પ્રયાસ કરું?")
                resp = executor.apply(scheme_id=scheme_id, profile=memory.profile, documents=documents)
            if resp["ok"]:
                memory.application = resp
                speak_gu(f"અરજી સ્વીકારાઈ. એપ્લિકેશન ID: {resp['application_id']}. સ્થિતિ: {resp['status']}.")
                state = State.CONFIRMATION
            else:
                speak_gu("સરવર સમસ્યા યથાવત છે. કૃપા કરીને થોડા સમય બાદ ફરી પ્રયાસ કરો.")
                state = State.END

        if state == State.CONFIRMATION:
            speak_gu("તમે SMS/ઈમેઇલ દ્વારા અપડેટ્સ મેળવશો. તમને બીજી કોઈ મદદ જોઈએ?")
            state = State.END

    speak_gu("આભાર! શુભેચ્છા.")

if __name__ == "__main__":
    run()
