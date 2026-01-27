# About

A template for a pushgateway service with or without persistent stoage and with or without tls.

The **PUSHGATEWAY_PERMANENT_STORAGE** environment variable (defaulting to "true") can be set to "false" for ephemeral storage. You should mount a volume at the path **/var/lib/pushgateway** in your extension to persist the pushgateway data.

The **PUSHGATEWAY_USE_TLS** environment variable (defaulting to "true") can be set to "false" to forgo tls. If enabled, You should mount a volume at the path **/etc/pushgateway/tls** with the following files: **server.crt**, **server.key** and **ca.crt**.


