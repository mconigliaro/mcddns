import os
import updatemyip.provider as provider


test_providers_path = os.path.join(os.path.dirname(__file__), "providers")
provider.import_modules(test_providers_path)
