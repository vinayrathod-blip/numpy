from .state_machine import State

class Planner:
    def decide(self, memory, user_text, last_state):
        text = (user_text or "").lower()

    
        if last_state == State.INIT:
            return State.COLLECT_PROFILE, "કૃપા કરીને તમારી મૂળભૂત વિગતો આપો: ઉંમર, જીલ્લો, માસિક આવક, અને વ્યવસાય."

        
        if last_state == State.COLLECT_PROFILE:
            missing = memory.get_missing_fields(["age", "district", "income_monthly", "occupation"])
            if missing:
                return State.COLLECT_PROFILE, f"પ્રથમ માહિતી જરૂરી છે: {', '.join(missing)} આપશો?"
            return State.RETRIEVE_SCHEMES, "તમારી માહિતી આધારે યોજનાઓ શોધી રહ્યો છું."


        if last_state == State.RETRIEVE_SCHEMES:
            return State.CHECK_ELIGIBILITY, "મળેલ યોજનાઓની પાત્રતા તપાસું છું."


        if last_state == State.RESOLVE_GAPS:
            return State.CHECK_ELIGIBILITY, "આભાર. હવે પાત્રતા ફરી તપાસું છું."

        
        if last_state == State.SELECT_SCHEME:
            if "અરજી" in text or "apply" in text or "હા" in text:
                return State.APPLY, "હવે અરજી શરૂ કરું છું."
            return State.SELECT_SCHEME, "શું પસંદ કરેલી યોજના માટે અરજી કરવી છે?"

        if last_state == State.CONFIRMATION:
            return State.END, "આભાર! વધુ મદદ જોઈએ તો કહો."

        
        return State.COLLECT_PROFILE, "કૃપા કરીને જણાવો કે કેવી સહાય જોઈએ છે."
