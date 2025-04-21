# Bedrock agents examples
In this repository, you learn about running agents using Amazon Bedrock. The repository contains different examples. All examples run as a notebook. Som of the code is in extra classes to make it easier to read.

## Essential parts of the code base
As the run_marketing_agent.ipynb notebook shows, there is little code required to call an agent and print the answer of the agent. Most of the work is setting up the _request_params_. The class `NonCollaboratingAgent` provides some details to make it easier for non collaborating agents to start.

Minimal requirements for an agent are:
- **Foundational model** - You can choose a model from Amazon Bedrock. The model is used to generate the response.
- **Introdcution** - The introduction is a short text tells the agents its purpose.
- **Session Id** - Through the session, the memory of the agent is kept. The session id is used to identify the session.


## Examples
The examples work in the Customer Relationship Management (CRM) domain. The examples are based on the following use cases:
- **Marketing Agent** answers questions about the company vision and mission.
- **Product expert Agent** knows everything about the products that we sell.
- **Order Support Agent** answers questions about the order status and order history.

The notebooks that show you the way to run agents are:
- **run_marketing_agent.ipynb**: This is a very basic agent that does not use any knowledge bases or action groups. It only uses the LLM to generate a response to questions about the company.


## References
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [Amazon Bedrock inline agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-create-inline.html)
- [Amazon Bedrock inline agents examples](https://github.com/awslabs/amazon-bedrock-agent-samples/tree/main/examples/agents/inline_agent)
- [OpenAI version of this blog](https://jettro.dev/create-a-multi-agent-system-with-openai-agent-sdk-a9c9fd618740)
- 