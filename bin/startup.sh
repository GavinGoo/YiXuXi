#!/bin/bash

YIXUXI_ARGS=""
YIXUXI_COMMAND="python main.py"

if [ -n "${YIXUXI_PORT}" ]; then
  YIXUXI_ARGS="${YIXUXI_ARGS} --port ${YIXUXI_PORT}"
fi

if [ -n "${YIXUXI_HOST}" ]; then
  YIXUXI_ARGS="${YIXUXI_ARGS} --host ${YIXUXI_HOST}"
fi

if [ -n "${YIXUXI_PROXY}" ]; then
  YIXUXI_ARGS="${YIXUXI_ARGS} --proxy ${YIXUXI_PROXY}"
fi

if [ -n "${YIXUXI_DEBUG}" ]; then
  YIXUXI_ARGS="${YIXUXI_ARGS} --debug"
fi

if [ -n "${YIXUXI_GPT_URL}" ]; then
  YIXUXI_ARGS="${YIXUXI_ARGS} --gpt-url ${YIXUXI_GPT_URL}"
fi

if [ -n "${YIXUXI_GPT_TOKEN}" ]; then
  YIXUXI_ARGS="${YIXUXI_ARGS} --gpt-token ${YIXUXI_GPT_TOKEN}"
fi

if [ -n "${YIXUXI_GPT_MODEL}" ]; then
  YIXUXI_ARGS="${YIXUXI_ARGS} --gpt-model ${YIXUXI_GPT_MODEL}"
fi

if [ -n "${YIXUXI_GLM_TOKEN}" ]; then
  YIXUXI_ARGS="${YIXUXI_ARGS} --gpt-token ${YIXUXI_GLM_TOKEN}"
fi

if [ -n "${YIXUXI_DEEPL_URL}" ]; then
  YIXUXI_ARGS="${YIXUXI_ARGS} --deepl-url ${YIXUXI_DEEPL_URL}"
fi

if [ -n "${YIXUXI_DEEPL_API}" ]; then
  YIXUXI_ARGS="${YIXUXI_ARGS} --deepl-api ${YIXUXI_DEEPL_API}"
fi

if [ -n "${YIXUXI_THREADS}" ]; then
  YIXUXI_ARGS="${YIXUXI_ARGS} --threads ${YIXUXI_THREADS}"
fi

if [ -n "${YIXUXI_LOG_SWITCH}" ]; then
  YIXUXI_ARGS="${YIXUXI_ARGS} --log"
fi

# shellcheck disable=SC2086
${YIXUXI_COMMAND} ${YIXUXI_ARGS}
