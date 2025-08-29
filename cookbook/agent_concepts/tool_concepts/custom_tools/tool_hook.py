"""Show how to use a tool execution hook, to run logic before and after a tool is called."""

import json
from typing import Dict

from agno.agent import Agent
from agno.tools.toolkit import Toolkit
from agno.utils.log import logger
from agno.models.ollama import Ollama

#------ 通过注册 class ，实现提供 多个 tool 给 agent
class CustomerDBTools(Toolkit):

    # 在 __init__ 方法中使用 self.register() 来注册每个工具方法, 才能被 agent 调用
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.retrieve_customer_profile)
        self.register(self.delete_customer_profile)

    def retrieve_customer_profile(self, customer_id: str):
        """
        Retrieves a customer profile from the database.

        Args:
            customer_id: The ID of the customer to retrieve.

        Returns:
            A string containing the customer profile.
        """
        logger.info(f"Looking up customer profile for {customer_id}")
        return json.dumps(
            {
                "customer_id": customer_id,
                "name": "John Doe",
                "email": "john.doe@example.com",
            }
        )

    def delete_customer_profile(self, customer_id: str):
        """
        Deletes a customer profile from the database.

        Args:
            customer_id: The ID of the customer to delete.
        """
        logger.info(f"Deleting customer profile for {customer_id}")
        return f"Customer profile for {customer_id}"


agent = Agent(
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    tools=[CustomerDBTools()],
    debug_mode=True,
    show_tool_calls=True,
)

# This should work
agent.print_response("I am customer 456, please retrieve my profile.")

# This should fail
agent.print_response("I am customer 123, please delete my profile.")
