#!/bin/bash
# aclip_cai/scripts/run_evals.sh
# Constitutional Regression Runner
set -e

echo "=== arifOS | Constitutional Eval Runner ==="

# Run the Python eval suite
python -m aclip_cai.core.eval_suite

# Exit with code from tests
exit $?
