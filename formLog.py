from pathlib import Path
import sys

def Convert(iname, wname):
    with Path(wname).open('w') as wf:
        with Path(iname).open() as f:
            for raw in f:
                if '##[endgroup]' in raw:
                    break
            for raw in f:
                #raw = raw.rstrip('\r\n')
                wf.write(raw[raw.find(' '):])

infile = [
    '2_Dump GitHub context.txt',
    '3_Dump job context.txt',
    '4_Dump steps context.txt',
    '5_Dump runner context.txt',
    '6_Dump strategy context.txt',
    '7_Dump matrix context.txt',
]
outfile = [
    '../../github_context_PLACEHOLDER.txt',
    '../../job_context_PLACEHOLDER.txt',
    '../../steps_context_PLACEHOLDER.txt',
    '../../runner_context_PLACEHOLDER.txt',
    '../../startegy_context_PLACEHOLDER.txt',
    '../../matrix_context_PLACEHOLDER.txt',
]

for i in range(0, len(infile)):
    Convert(infile[i], outfile[i].replace('PLACEHOLDER', 'wiki_edit_page'))


        
