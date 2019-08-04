from uranium import current_build
import os

current_build.packages.install("uranium-plus[vscode]")
import uranium_plus

current_build.config.update({"uranium-plus": {"module": "vcver"}})

uranium_plus.bootstrap(current_build)
