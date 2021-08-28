from aws_cdk import aws_lambda, aws_ssm, aws_events, aws_events_targets, core

class UnreadGmailWatcherStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 認証トークン
        slack_bot_token = aws_ssm.StringParameter.from_string_parameter_attributes(self, 'slack-bot-token',
            parameter_name = '/unread-gmail-watcher/SLACK_BOT_TOKEN'
        ).string_value
        
        # 送信先のチャンネル名
        slack_channel = aws_ssm.StringParameter.from_string_parameter_attributes(self, 'slack-channel',
            parameter_name = '/unread-gmail-watcher/SLACK_CHANNEL'
        ).string_value

        # Lambdaレイヤー
        lambda_layer = aws_lambda.LayerVersion(
            self,
            'lambda-layer',
            compatible_runtimes = [aws_lambda.Runtime.PYTHON_3_7],
            code = aws_lambda.AssetCode('lambda/layers')
        )
        
        # 各種設定値
        params = dict(
            runtime = aws_lambda.Runtime.PYTHON_3_7,
            handler = 'lambda_function.lambda_handler',
            timeout = core.Duration.seconds(60),
            memory_size = 256,
        )

        # Lambda関数
        lambda_function = aws_lambda.Function(
            self,
            'lambda-function',
            code = aws_lambda.Code.asset('lambda/functions'),
            layers = [lambda_layer],
            environment = {
                'SLACK_BOT_TOKEN': slack_bot_token,
                'SLACK_CHANNEL': slack_channel
            },
            **params
        )

        # EventBrdge
        event_bridge = aws_events.Rule(
            self,
            'event-bridge',
            schedule = aws_events.Schedule.cron(
                minute='30',
                hour='*',
                month='*',
                year='*'
            )
        )
        
        event_bridge.add_target(aws_events_targets.LambdaFunction(lambda_function))
