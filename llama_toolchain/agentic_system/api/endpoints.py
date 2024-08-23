# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from .datatypes import *  # noqa: F403
from typing import Protocol

from llama_models.schema_utils import json_schema_type, webmethod


@json_schema_type
class AgenticSystemCreateResponse(BaseModel):
    agent_id: str


@json_schema_type
class AgenticSystemSessionCreateResponse(BaseModel):
    session_id: str


@json_schema_type
class AgenticSystemTurnCreateRequest(AgentConfigOverridablePerTurn):
    agent_id: str
    session_id: str

    # TODO: figure out how we can simplify this and make why
    # ToolResponseMessage needs to be here (it is function call
    # execution from outside the system)
    messages: List[
        Union[
            UserMessage,
            ToolResponseMessage,
        ]
    ]
    attachments: Optional[List[Attachment]] = None

    stream: Optional[bool] = False


@json_schema_type(
    schema={"description": "Server side event (SSE) stream of these events"}
)
class AgenticSystemTurnResponseStreamChunk(BaseModel):
    event: AgenticSystemTurnResponseEvent


@json_schema_type
class AgenticSystemStepResponse(BaseModel):
    step: Step


class AgenticSystem(Protocol):
    @webmethod(route="/agentic_system/create")
    async def create_agentic_system(
        self,
        agent_config: AgentConfig,
    ) -> AgenticSystemCreateResponse: ...

    @webmethod(route="/agentic_system/turn/create")
    async def create_agentic_system_turn(
        self,
        request: AgenticSystemTurnCreateRequest,
    ) -> AgenticSystemTurnResponseStreamChunk: ...

    @webmethod(route="/agentic_system/turn/get")
    async def get_agentic_system_turn(
        self,
        agent_id: str,
        turn_id: str,
    ) -> Turn: ...

    @webmethod(route="/agentic_system/step/get")
    async def get_agentic_system_step(
        self, agent_id: str, turn_id: str, step_id: str
    ) -> AgenticSystemStepResponse: ...

    @webmethod(route="/agentic_system/session/create")
    async def create_agentic_system_session(
        self,
        agent_id: str,
        session_name: str,
    ) -> AgenticSystemSessionCreateResponse: ...

    @webmethod(route="/agentic_system/session/get")
    async def get_agentic_system_session(
        self,
        agent_id: str,
        session_id: str,
        turn_ids: Optional[List[str]] = None,
    ) -> Session: ...

    @webmethod(route="/agentic_system/session/delete")
    async def delete_agentic_system_session(
        self, agent_id: str, session_id: str
    ) -> None: ...

    @webmethod(route="/agentic_system/delete")
    async def delete_agentic_system(
        self,
        agent_id: str,
    ) -> None: ...
