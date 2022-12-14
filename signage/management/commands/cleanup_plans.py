from django.core.management.base import BaseCommand
from django.utils import timezone
from signage.api import fetch_plans_list
from signage.models import Plan

class Command(BaseCommand):
    help = 'Cleanup plans from local db'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.cleanup()
        self.stdout.write("Cleanup complete!")
    

    def cleanup(self):
        response =  fetch_plans_list()
        plans = response["data"]

        plan_ids = []
        for plan in plans:
            plan_ids.append(plan["id"])
       
        # Get plans from local db
        invalid_plans = Plan.objects.exclude(plan_id__in = plan_ids)
        print(invalid_plans)

        for plan in invalid_plans:
            plan.delete()
    
        

