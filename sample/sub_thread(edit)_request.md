EVENT HEADER
```json
{
  "Accept": "*/*",
  "Accept-Encoding": "gzip,deflate",
  "Content-Type": "application/json",
  "Content-Length": "1579",
  "Host": "dauden.cloud",
  "User-Agent": "Slackbot 1.0 (+https://api.slack.com/robots)",
  "X-Slack-Signature": "v0=0667248696bc46c97b8a7c751b26021e89f3056dc6b6f2b20c2ac726d15c420b",
  "X-Slack-Request-Timestamp": "1715405196"
}
```


EVENT POSTBODY
```json
{
  "token": "OifjAOHsLCZZ3u8wvqUF4o7s",
  "team_id": "TAGSCCP7Z",
  "context_team_id": "TAGSCCP7Z",
  "context_enterprise_id": null,
  "api_app_id": "A071NP30LCU",
  "event": {
    "type": "message",
    "subtype": "message_changed",
    "message": {
      "user": "U07244Q1EHG",
      "type": "message",
      "edited": {
        "user": "U07244Q1EHG",
        "ts": "1715405196.000000"
      },
      "client_msg_id": "6cb0fa34-d090-455e-9319-a5fd1d99cca1",
      "text": "Hello sub message (edit)",
      "team": "TAGSCCP7Z",
      "thread_ts": "1715405022.898079",
      "parent_user_id": "U07244Q1EHG",
      "blocks": [
        {
          "type": "rich_text",
          "block_id": "sUDHB",
          "elements": [
            {
              "type": "rich_text_section",
              "elements": [
                {
                  "type": "text",
                  "text": "Hello sub message (edit)"
                }
              ]
            }
          ]
        }
      ],
      "ts": "1715405083.488449",
      "source_team": "TAGSCCP7Z",
      "user_team": "TAGSCCP7Z"
    },
    "previous_message": {
      "user": "U07244Q1EHG",
      "type": "message",
      "ts": "1715405083.488449",
      "client_msg_id": "6cb0fa34-d090-455e-9319-a5fd1d99cca1",
      "text": "Hello sub message",
      "team": "TAGSCCP7Z",
      "thread_ts": "1715405022.898079",
      "parent_user_id": "U07244Q1EHG",
      "blocks": [
        {
          "type": "rich_text",
          "block_id": "lWmEG",
          "elements": [
            {
              "type": "rich_text_section",
              "elements": [
                {
                  "type": "text",
                  "text": "Hello sub message"
                }
              ]
            }
          ]
        }
      ]
    },
    "channel": "C071P11UWHJ",
    "hidden": true,
    "ts": "1715405196.000400",
    "event_ts": "1715405196.000400",
    "channel_type": "channel"
  },
  "type": "event_callback",
  "event_id": "Ev072TD1MECW",
  "event_time": 1715405196,
  "authorizations": [
    {
      "enterprise_id": null,
      "team_id": "TAGSCCP7Z",
      "user_id": "UAF8W1P33",
      "is_bot": false,
      "is_enterprise_install": false
    }
  ],
  "is_ext_shared_channel": false,
  "event_context": "4-eyJldCI6Im1lc3NhZ2UiLCJ0aWQiOiJUQUdTQ0NQN1oiLCJhaWQiOiJBMDcxTlAzMExDVSIsImNpZCI6IkMwNzFQMTFVV0hKIn0"
}
```