from airflow.models import Variable
from slack_sdk import WebClient
"""
To use the SlackWebhookOperator set up a Slack bot with inbound webhooks
Install into your slack workspace
Create new connection from the admin/connections
Set the Conn Id as 'slack'
Conn Type as 'http'
Host as 'https://hooks.slack.com/services'
Password as everything else after the host mentioned above
STAGING_LINK set if you were running Airflow locally
"""

ADMIN_URL = Variable.get("AIRFLOW_ADMIN_URL")
SLACK_BOT_TOKEN = Variable.get("SLACK_BOT_TOKEN")


def switch_urls(context) -> str:
    log_url = context.get("task_instance").log_url
    ix = log_url.find("log?")  # finding the beginning of the important stuff
    return ADMIN_URL + log_url[ix:]


def success_alert(channel: str) -> callable:
    def success(context):
        """
        Alerts when all tasks succeed
        Args:
            channel (str): Channel to send message to
            context (dict): Context variable passed in from Airflow natively
        Returns:
            None: Calls Slack's web client chat_postMessage method internally
        """
        exec_time = context.get("execution_date")
        cleaned_ts = exec_time.strftime("%x %X")

        slack_msg = (
            f':green-light: Task successful!\n'
            f'*DAG*: {context.get("task_instance").dag_id}\n'
            f'*Execution Time*: {cleaned_ts}\n'
            f'*Task Id*: {context.get("task_instance").task_id}\n'
            f'*Logs*: {switch_urls(context)}'
        )

        client = WebClient(token=SLACK_BOT_TOKEN)

        client.chat_postMessage(channel=f"#{channel}", text=slack_msg)
    return success


def failure_alert(channel: str) -> callable:
    def failure(context):
        """
        Alerts when all tasks fail
        Args:
            channel (str): Channel to send message to
            context (dict): Context variable passed in from Airflow natively
        Returns:
            None: Calls Slack's web client chat_postMessage method internally
        """
        exec_time = context.get("execution_date")
        cleaned_ts = exec_time.strftime("%x %X")

        slack_msg = (
            f':red-card: Task failed!\n'
            f'*DAG*: {context.get("task_instance").dag_id}\n'
            f'*Execution Time*: {cleaned_ts}\n'
            f'*Logs*: {switch_urls(context)}'
        )

        client = WebClient(token=SLACK_BOT_TOKEN)

        client.chat_postMessage(channel=f"#{channel}", text=slack_msg)
    return failure
