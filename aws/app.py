#!/usr/bin/env python3

from aws_cdk import core

from stacks.unread_gmail_watcher_stack import UnreadGmailWatcherStack

app = core.App()

UnreadGmailWatcherStack(app, 'unread-gmail-watcher-stack')

app.synth()
