## Welcome to the build planner project!

To set up your development environment, simply run the script `./scripts/setup.sh`. This will work on Mac or linux. The
scripts directory also contains handy scripts for linting, formatting & running tests.

To visualise a wall build, run the script `./scripts/run_visualiser.sh`. This will show you the entire wall in light
grey and will play the build step by step as you press `return`. You can run `./scripts/run_visualiser -h` to see all
the program options. With the given movement and alignment strategies, it places as many bricks per stride as possible.
The most optimal strategies have been set as the defaults for each bond type.

To work out which move and alignment strategies are most optimal (in terms of strides) for a particular wall, run the
script `./scripts/run_planner.sh`. This will take the product of all supported move and alignment strategies and output
the number of strides that were needed. You can run `./scripts/run_planner -h` to see all the program options.

We use uv as the package and project manager. For more info, see here: https://docs.astral.sh/uv/
