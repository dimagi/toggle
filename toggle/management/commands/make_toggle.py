from optparse import make_option
from django.core.management.base import LabelCommand, CommandError, BaseCommand
from ...models import Toggle, ENTITY_TYPES


class Command(BaseCommand):
    help = "Makes a toggle."
    args = "<slug> -t <type> *<users>"
    label = ""
    option_list = BaseCommand.option_list + (
        make_option("-t", "--type", action="store", type="string", dest="entity_type",
            help="Denotes the type of entity"),
        )
     
    def handle(self, *args, **options):
        if len(args) < 1:
            raise CommandError('Have to specify a toggle slug.')
        slug = args[0]
        entity_type = options.get('entity_type') or 'user'
        if entity_type not in ENTITY_TYPES.keys():
            print "Unsupported entity type. Supported types: {types}".format(types=ENTITY_TYPES.keys())
            return

        entities = list(args[1:])
        kwargs = {"slug": slug, ENTITY_TYPES[entity_type]: entities}
        toggle = Toggle(**kwargs)
        toggle.save()
        print "Created toggle named '{slug}' for entities of type '{entity_type}'".format(slug=slug, entity_type=entity_type)


