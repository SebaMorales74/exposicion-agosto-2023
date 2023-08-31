from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import ConnectEvent, CommentEvent, GiftEvent, ShareEvent, LikeEvent, FollowEvent, ViewerUpdateEvent

try:
    client: TikTokLiveClient = TikTokLiveClient(unique_id='abuelita_juliana')
except Exception as e:
    print(f'❌ Hubo un error al conectarse con TikTok: {e}')


@client.on('connect')
async def on_connect(_: ConnectEvent):
    print('✔️ Conectado a TikTokLive')


@client.on('comment')
async def on_comment(event: CommentEvent):
    print(f"💬 @{event.user.unique_id} -> {event.comment}")


@client.on('gift')
async def on_gift(event: GiftEvent):
    print(f"🎁 @{event.user.unique_id} mandó un regalo de {event.gift.info.name}")


@client.on('like')
async def on_like(event: LikeEvent):
    print(
        f'❤️  @{event.user.unique_id} le dió me gusta (Cantidad total de me gusta: {event.total_likes})')


@client.on('share')
async def on_share(event: ShareEvent):
    print(f"📣  @{event.user.unique_id} compartió el live")


@client.on('follow')
async def on_follow(event: FollowEvent):
    print(f"🥑  @{event.user.unique_id} acaba de dar follow")

if __name__ == "__main__":
    client.run()
