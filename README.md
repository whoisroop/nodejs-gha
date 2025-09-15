# GitHub Actions Workflow Guide

This document explains the structure and usage of GitHub Actions workflow files, including triggers, context objects, outputs, environment variables, filters, and conditional logic.

## Workflow File Structure

```yaml
name: <Name Of WorkFlow>
on: <Trigger>
jobs:
  <JOB NAME>:
    runs-on: <Runner>
    steps:
      - name: <STEP NAME>
        run: <Command>
```

## Workflow Triggers

Besides repository events (push, pull_request, etc.), workflows can be triggered by:

1. **workflow_dispatch**: Manual trigger
2. **repository_dispatch**: API trigger
3. **schedule**: Runs on a schedule
4. **workflow_call**: Triggered by another workflow

## Expression & Context Objects

Context objects are special variables available inside workflows. They provide information about the workflow, runner, jobs, events, and secrets. Rendering of context objects/expressions occurs before execution.

Example:
```yaml
jobs.steps.run: echo "${{ github }}"
```

Common context objects:
- `github`
- `secrets`
- `env`
- `needs`
- `runner`
- `matrix`
- Conditionals: `if: always()`, `success()`, `failure()`

## GitHub Actions Output & Environment

Set outputs and environment variables for use in subsequent steps:

```bash
echo "color=YELLOW" >> $GITHUB_OUTPUT
# Access: ${{ steps.<STEP NAME>.outputs.color }}

echo "MYTOKEN=xxx" >> $GITHUB_ENV

echo "/opt/mytool/bin" >> $GITHUB_PATH  # Prepend directories to PATH
```

## Event Trigger Types

Specify which activity type should trigger the event (e.g., pull_request opened, edited, closed):

```yaml
on:
  pull_request:
    types:
      - opened
```

## Filters

Define triggers for specific branches, directories, or files:

```yaml
on:
  push:
    branches:
      - main
      - 'feature/**'  # **: Zero or multiple directories
    tags:
      - 'release/*'
    paths-ignore:
      - '.github/workflows/*'
```

Supported for `pull_request`, `push`, `workflow_call`:
- `branches`, `tags`, `branches-ignore`, `tags-ignore`
- `paths`, `paths-ignore`

**Note:** Pull requests from forked repositories require manual approval for the first-time contributor.

## Skipping Workflows

Workflows are skipped if the commit message contains any of:
- `[skip ci]`
- `ci skip`
- `no ci`
- `skip actions`
- `actions skip`

Example:
```
Added Comments [skip ci]
```

## Conditional Jobs & Steps

- Use `if` for conditional jobs and steps
- Use `continue-on-error` for steps to ignore errors
