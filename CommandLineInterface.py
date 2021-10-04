import os

import click

import Configuration

@click.command()
@click.option('--in-file', '-i', default = os.path.join(Configuration.project_filepath, 'input', 'darmstadt-scenario.xml'),
              help='Path to scenario.xml input file to be processed'
              )
@click.option('--out-file', '-o', default= os.path.join(Configuration.project_filepath, 'output', 'out.xml'),
              help='Path to the output result xml file.')
@click.option('--config-file', '-c', default=os.path.join(Configuration.project_filepath, 'config', 'config.yaml'),
              help='Path to configuration file')
@click.option('--random-mode', '-r', default=False,
              help='Starts the simulation with a random scenario (--in-file argument will be ignored)')
def process(in_file, out_file, config_file, random_mode):
    ''' RGBSim Command Line Interface (CLI) - Processes the given scenario and returns the simulation results.
    '''
    print('input    ' + in_file)
    print('output   ' + out_file)
    print('config   ' + config_file)
    print('random-mode  ' + str(random_mode))

    Configuration.initialize_configuration(in_file, out_file, config_file, random_mode)

    # Execute needs to be imported here instead of at the beginning of this .py file,
    # because it needs the configuration initialized first
    import Execute
    Execute.main()

# This is the actual implementation of the simulation. The code above is just the definition of the CLI
def process_simulation(in_file, out_file, config_file, random_mode):
    Configuration.initialize_configuration(in_file, out_file, config_file, random_mode)

    # Execute needs to be imported here instead of at the beginning of this .py file,
    # because it needs the configuration initialized first
    import Execute
    Execute.main()

if __name__ == '__main__':
    process()
