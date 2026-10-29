from django.core.management.base import BaseCommand

from core.models import Event


class Command(BaseCommand):
    help = "Fix duplicate position values in EventPageMenu for all events"

    def handle(self, *args, **options):
        fixed_count = 0
        error_count = 0

        for event in Event.all_objects.all():
            menus = event.menu.all().order_by("position", "id")
            positions = list(menus.values_list("position", flat=True))

            # Check if there are duplicates
            if len(positions) != len(set(positions)):
                self.stdout.write(
                    self.style.WARNING(f"Event {event.id} ({event.name}) has duplicate positions")
                )

                # Reassign positions sequentially
                for index, menu in enumerate(menus, start=1):
                    old_position = menu.position
                    if old_position != index:
                        menu.position = index
                        menu.save()
                        self.stdout.write(
                            f"  Menu {menu.id} ({menu.title}): {old_position} -> {index}"
                        )
                        fixed_count += 1

        self.stdout.write(self.style.SUCCESS(f"\nTotal menu items fixed: {fixed_count}"))
