from google.adk.agents import Agent
from google.adk.tools.bigquery import BigQueryCredentialsConfig
from google.adk.tools.bigquery import BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig
from google.adk.tools.bigquery.config import WriteMode
import google.auth
import vertexai

# Define constants for this example agent
AGENT_NAME = "bigquery_agent"
GEMINI_MODEL = "gemini-2.0-flash"

vertexai.init(
    project="gen-xxx-7433693",
    location="us-central1",
    staging_bucket="gs://agent-xxxx-12025",
)

# Define a tool configuration to block any write operations
tool_config = BigQueryToolConfig(write_mode=WriteMode.BLOCKED)

# Define a credentials config - in this example we are using application default credentials
# https://cloud.google.com/docs/authentication/provide-credentials-adc
application_default_credentials, _ = google.auth.default()
credentials_config = BigQueryCredentialsConfig(
    credentials=application_default_credentials
)

# Instantiate a BigQuery toolset
bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config, bigquery_tool_config=tool_config
)

# Agent Definition
root_agent = Agent(
    model=GEMINI_MODEL,
    name=AGENT_NAME,
    description=(
        "Agent to answer questions about BigQuery data and models and execute SQL queries."
    ),
    instruction="""\
        You are a data science agent with access to several BigQuery tools.
        Make use of those tools ONLY to answer the user's questions. If you are not able to find the details
        in big query tables, then update the user as not able to find the relevant information.
    """,
    tools=[bigquery_toolset],
)

bigquery_toolset = BigQueryToolset(credentials_config=credentials_config,   tool_filter=[
'list_dataset_ids',
'get_dataset_info',
'list_table_ids',
'get_table_info',
'execute_sql',
     ])

