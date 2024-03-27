# chat/consumers.py
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import LifeTracker
from .serializers import LifeTrackerSerializer


class LifeTrackerConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "lifetracker"
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        life_tracker_exists = await self._get_life_tracker_exists()
        if not life_tracker_exists:
            await self._create_init_life_tracker()
        life_tracker_data = await self._get_current_life_tracker_data()
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "send.life", "message": life_tracker_data}
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive_json(self, content, **kwargs):
        player = content.get("player", None)
        amount_update = content.get("amount_update", None) or 0
        name = content.get("name", None) or ""
        if amount_update:
            await self._update_life(player, amount_update)
        if name:
            await self._update_name(player, name)

        life_tracker_data = await self._get_current_life_tracker_data()
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "send.life", "message": life_tracker_data}
        )

    async def send_life(self, event):
        life_tracker_data = event["message"]
        await self.send_json(json.dumps(life_tracker_data))

    @database_sync_to_async
    def _update_name(self, player_update: str, name: str):
        life_tracker = LifeTracker.objects.first()
        if player_update == "p1":
            life_tracker.p1_name = name
        if player_update == "p2":
            life_tracker.p2_name = name
        life_tracker.save()

    @database_sync_to_async
    def _update_life(self, player_update: str, amount_update: int):
        life_tracker = LifeTracker.objects.first()
        if player_update == "p1":
            life_tracker.p1_life = life_tracker.p1_life + amount_update
        else:
            life_tracker.p2_life = life_tracker.p2_life + amount_update
        life_tracker.save()

    @database_sync_to_async
    def _get_life_tracker_exists(self):
        return LifeTracker.objects.exists()

    @database_sync_to_async
    def _create_init_life_tracker(self):
        LifeTracker.objects.create(
            p1_life=40, p2_life=40, p1_name="Player 1", p2_name="Player 2"
        )

    @database_sync_to_async
    def _get_current_life_tracker_data(self):
        life_tracker = LifeTracker.objects.first()
        return LifeTrackerSerializer(instance=life_tracker).data
