#!/usr/bin/env bash
set -Eeuo pipefail

CAN_INTERFACE="${IGINNO_CAN_INTERFACE:-can1}"
CAN_BITRATE="${IGINNO_CAN_BITRATE:-500000}"
CAN_REQUIRED="${IGINNO_CAN_REQUIRED:-0}"
CAN_AUTOLOAD="${IGINNO_CAN_AUTOLOAD:-1}"
CAN_MODULE_NAME="${IGINNO_CAN_MODULE_NAME:-gs_usb}"
CAN_MODULE_PATH="${IGINNO_CAN_MODULE_PATH:-/home/hcic/ros2_ws/src/robot_nav/can_tool/gs_usb.ko}"
CAN_WAIT_SEC="${IGINNO_CAN_WAIT_SEC:-5}"

if [[ "${IGINNO_CAN_SETUP:-1}" == "0" ]]; then
  echo "IG Inno CAN setup disabled by IGINNO_CAN_SETUP=0"
  exit 0
fi

if [[ ! "${CAN_INTERFACE}" =~ ^[a-zA-Z0-9_.:-]+$ ]]; then
  echo "Invalid CAN interface name: ${CAN_INTERFACE}" >&2
  exit 1
fi
if [[ ! "${CAN_BITRATE}" =~ ^[0-9]+$ ]] || (( CAN_BITRATE <= 0 )); then
  echo "Invalid CAN bitrate: ${CAN_BITRATE}" >&2
  exit 1
fi
if [[ ! "${CAN_REQUIRED}" =~ ^[01]$ ]]; then
  echo "IGINNO_CAN_REQUIRED must be 0 or 1" >&2
  exit 1
fi
if [[ ! "${CAN_AUTOLOAD}" =~ ^[01]$ ]]; then
  echo "IGINNO_CAN_AUTOLOAD must be 0 or 1" >&2
  exit 1
fi
if [[ ! "${CAN_MODULE_NAME}" =~ ^[a-zA-Z0-9_]+$ ]]; then
  echo "Invalid CAN module name: ${CAN_MODULE_NAME}" >&2
  exit 1
fi
if [[ ! "${CAN_WAIT_SEC}" =~ ^[0-9]+$ ]] || (( CAN_WAIT_SEC > 60 )); then
  echo "IGINNO_CAN_WAIT_SEC must be an integer from 0 to 60" >&2
  exit 1
fi

can_interface_exists() {
  ip link show dev "${CAN_INTERFACE}" >/dev/null 2>&1
}

can_module_loaded() {
  grep -qE "^${CAN_MODULE_NAME}[[:space:]]" /proc/modules
}

if ! can_interface_exists && [[ "${CAN_AUTOLOAD}" == "1" ]]; then
  if can_module_loaded; then
    echo "CAN module ${CAN_MODULE_NAME} is already loaded; waiting for ${CAN_INTERFACE}"
  elif modprobe -q "${CAN_MODULE_NAME}"; then
    echo "Loaded CAN module with modprobe: ${CAN_MODULE_NAME}"
  elif [[ -f "${CAN_MODULE_PATH}" ]]; then
    echo "Loading factory-provided CAN module: ${CAN_MODULE_PATH}"
    if ! insmod "${CAN_MODULE_PATH}" && ! can_module_loaded; then
      echo "Failed to load CAN module: ${CAN_MODULE_PATH}" >&2
    fi
  else
    echo "CAN module is unavailable: ${CAN_MODULE_PATH}" >&2
  fi

  for ((attempt = 0; attempt < CAN_WAIT_SEC * 4; attempt++)); do
    can_interface_exists && break
    sleep 0.25
  done
fi

if ! can_interface_exists; then
  if [[ "${CAN_REQUIRED}" == "0" ]]; then
    echo "CAN interface ${CAN_INTERFACE} is absent; continuing because IGINNO_CAN_REQUIRED=0"
    exit 0
  fi
  echo "Required CAN interface ${CAN_INTERFACE} does not exist" >&2
  exit 1
fi

CAN_LINK_LINE="$(ip -o link show dev "${CAN_INTERFACE}")"
CAN_LINK_FLAGS="${CAN_LINK_LINE#*<}"
CAN_LINK_FLAGS="${CAN_LINK_FLAGS%%>*}"
CAN_LINK_DETAILS="$(ip -details link show dev "${CAN_INTERFACE}")"
case ",${CAN_LINK_FLAGS}," in
  *,UP,*)
    if grep -qE "bitrate[[:space:]]+${CAN_BITRATE}([[:space:]]|$)" <<<"${CAN_LINK_DETAILS}"; then
      echo "CAN interface ${CAN_INTERFACE} is already UP at ${CAN_BITRATE} bit/s"
      printf '%s\n' "${CAN_LINK_DETAILS}"
      exit 0
    fi
    echo "CAN interface ${CAN_INTERFACE} is UP with a different bitrate; reconfiguring"
    ;;
esac

ip link set dev "${CAN_INTERFACE}" down
ip link set dev "${CAN_INTERFACE}" type can bitrate "${CAN_BITRATE}"
ip link set dev "${CAN_INTERFACE}" up
ip -details link show dev "${CAN_INTERFACE}"