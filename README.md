# instatus-minecraft

Queries a Minecraft server instance and sends the playercount as metric to Instatus to visualize your server's playercount on your Instatus page.

As seen on [MCC's status page](https://status.mcchampionship.com).

<img width="1640" height="586" alt="CleanShot 2025-07-17 at 22 14 59@2x" src="https://github.com/user-attachments/assets/18513bb0-599f-434a-86bc-7ee3c407363f" />


## Usage

A Docker image is available at `ghcr.io/noxcrew/instatus-minecraft:latest`. Configure it with the environment variables below.

## Configuration / Environment Variables

- INSTATUS_PAGE_ID: The unique identifier for the Instatus status page.
- INSTATUS_METRIC_ID: The unique identifier for the metric to update on Instatus.
- INSTATUS_TOKEN: The authentication token used to access the Instatus API.
- MC_SERVER_IP: The IP address of the Minecraft server to monitor. Defaults to "play.mccisland.net".
- QUERY_INTERVAL: The interval (in seconds) between server status queries. Defaults to "30".
