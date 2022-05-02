import subprocess
from datetime import timedelta, timezone

JST = timezone(timedelta(hours=+9), 'JST')
AWS_AZ = subprocess.run(["curl", "-s", "http://169.254.169.254/latest/meta-data/placement/availability-zone"], stdout=subprocess.PIPE, text=True).stdout
AWS_REGION = AWS_AZ[:-1]
