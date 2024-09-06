#!/usr/bin/env python

import click
import os

def get_bytes_count(input_path):
    return os.stat(input_path).st_size

def get_lines_count(input_path):
    with open(input_path) as f:
        return sum(1 for line in f)

def get_words_count(input_path):
    with open(input_path) as f:
        return sum(len(line.split()) for line in f)
    
def get_chars_count(input_path):
    with open(input_path) as f:
        input = f.read()
        return len(input) + input.count('\n')

@click.command()
@click.option('-c', 'bytes_count', is_flag=True)
@click.option('-w', 'words_count', is_flag=True)
@click.option('-l', 'lines_count', is_flag=True)
@click.option('-m', 'chars_count', is_flag=True)
@click.argument('input_path', type=click.Path(), default='-')
def word_count(bytes_count, words_count, lines_count, chars_count, input_path):
    if input_path == '-':
        input_path = '/dev/stdin'
    counts = []
    if lines_count:
        counts.append(get_lines_count(input_path))
    if words_count:
        counts.append(get_words_count(input_path))
    if chars_count:
        counts.append(get_chars_count(input_path))
    elif bytes_count: # Mirroring wc behavior. If -c and -m are both specified, -c is ignored
        counts.append(get_bytes_count(input_path))
    if len(counts) == 0:
        counts = [get_lines_count(input_path), get_words_count(input_path), get_bytes_count(input_path)]

    output = "   ".join(str(count) for count in counts)
    output = f'    {output} {os.path.basename(input_path)}'

    click.echo(output)

if __name__ == '__main__':
    word_count()