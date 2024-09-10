import click

STD_INPUT = '/dev/stdin'

def is_empty_line(line):
    return line in ['\n', '\r\n']


@click.command()
@click.option("-n", "include_line_numbers", is_flag=True)
@click.option("-b", "include_line_numbers_excluding_empty_lines", is_flag=True)
@click.argument('input_paths', type=click.Path(), nargs=-1)
def cat(include_line_numbers, include_line_numbers_excluding_empty_lines, input_paths):

    number_empty_lines = True
    if include_line_numbers_excluding_empty_lines:
        number_empty_lines = False
        include_line_numbers = True

    if len(input_paths) == 0:
        input_paths = ['-',]

    for input_path in input_paths:
        if input_path == '-':
            input_path = STD_INPUT
        with open(input_path) as f:
            lno = 1
            for line in f:
                if not include_line_numbers or (is_empty_line(line) and not number_empty_lines):
                    click.echo(line, nl=False)
                else:
                    click.echo(f'{lno} {line}', nl=False)
                    lno += 1

if __name__ == '__main__':
    cat()