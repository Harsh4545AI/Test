from typing import Dict, List
from dataclasses import dataclass
from pydantic_ai import messages as _m
from uuid import UUID
from datetime import datetime

@dataclass(frozen=True, slots=True)
class HistoryKey:
    user_id: str
    session_id: UUID
    agent_name: str

class AgentMemoryCoordinator:
    def __init__(self, agent_specs: Dict[str, any]):
        self._histories: Dict[HistoryKey, List[_m.ModelMessage]] = {}
        self.agent_specs = agent_specs

    def get_history(self, user_id: str, session_id: UUID, agent_name: str) -> List[_m.ModelMessage]:
        key = HistoryKey(user_id, session_id, agent_name)
        return self._histories.setdefault(key, self._init_history(agent_name))

    def _init_history(self, agent_name: str) -> List[_m.ModelMessage]:
        system_prompt = self.agent_specs[agent_name].system_prompt
        return [_m.ModelRequest(parts=[_m.SystemPromptPart(content=system_prompt)])]

    def update_history(self, user_id: str, session_id: UUID, agent_name: str, new_msgs: List[_m.ModelMessage]):
        key = HistoryKey(user_id, session_id, agent_name)
        history = self.get_history(user_id, session_id, agent_name)
        history.extend(new_msgs)
        self._trim(history)

    def _trim(self, history: List[_m.ModelMessage], keep_last: int = 20):
        if len(history) > keep_last + 1:
            history[:] = [history[0]] + history[-keep_last:]

    def rebase_history_for_agent(self, from_agent: str, to_agent: str, user_id: str, session_id: UUID) -> List[_m.ModelMessage]:
        source_history = self.get_history(user_id, session_id, from_agent)
        system_prompt = self.agent_specs[to_agent].system_prompt
        system_part = _m.SystemPromptPart(content=system_prompt)

        rebased = []
        for i, msg in enumerate(source_history):
            if isinstance(msg, _m.ModelRequest):
                user_parts = [p for p in msg.parts if isinstance(p, _m.UserPromptPart)]
                if i == 0:
                    rebased.append(_m.ModelRequest(parts=[system_part] + user_parts))
                else:
                    rebased.append(_m.ModelRequest(parts=user_parts))
            elif isinstance(msg, _m.ModelResponse):
                rebased.append(msg)

        return rebased
