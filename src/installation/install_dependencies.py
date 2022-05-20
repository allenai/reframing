import sys
import subprocess

dependencies = ['sacrebleu', 'rouge_score', 'datasets', 'git+https://github.com/google-research/bleurt.git']
for i in dependencies:
# implement pip as a subprocess:
  subprocess.check_call([sys.executable, '-m', 'pip', 'install', i])