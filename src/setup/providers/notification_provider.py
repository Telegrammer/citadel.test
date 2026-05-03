from celery import Celery
from dishka import Provider, Scope, provide

from application.ports.notifiers import (
    UserActivationKeyGeneratedNotifier,
    VirtualMachineClaimedNotifier,
    VirtualMachineFreedNotifier,
)
from application.ports.subscribers import ConnectionStatusSubscriber
from infrastructure.adapters.notifiers import (
    CeleryUserActivationKeyGeneratedNotifier,
    RedisVirtualMachineClaimedNotifier,
    RedisVirtualMachineFreedNotifier,
)
from infrastructure.adapters.subscribers import RedisConnectionStatusSubscriber
from infrastructure.adapters.task_queue import NotificationTaskQueue


class NotificationProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_celery_app(self) -> Celery:
        from setup.celery_app import celery_app

        return celery_app

    notification_task_queue = provide(NotificationTaskQueue)
    activation_key_notifier = provide(
        source=CeleryUserActivationKeyGeneratedNotifier,
        provides=UserActivationKeyGeneratedNotifier,
        scope=Scope.REQUEST,
    )
    virtual_machine_claimed_notifier = provide(
        source=RedisVirtualMachineClaimedNotifier,
        provides=VirtualMachineClaimedNotifier,
        scope=Scope.REQUEST,
    )
    virtual_machine_freed_notifier = provide(
        source=RedisVirtualMachineFreedNotifier,
        provides=VirtualMachineFreedNotifier,
        scope=Scope.REQUEST,
    )
    connection_status_subscriber = provide(
        source=RedisConnectionStatusSubscriber,
        provides=ConnectionStatusSubscriber,
        scope=Scope.SESSION,
    )
