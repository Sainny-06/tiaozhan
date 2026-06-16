import type { PackageGenerateResponse } from '../types/package'

const RECENT_PACKAGE_KEY = 'zhixue_recent_package'

export function saveRecentPackage(packageResult: PackageGenerateResponse) {
  localStorage.setItem(RECENT_PACKAGE_KEY, JSON.stringify(packageResult))
}

export function loadRecentPackage(): PackageGenerateResponse | null {
  const raw = localStorage.getItem(RECENT_PACKAGE_KEY)
  if (!raw) {
    return null
  }

  try {
    return JSON.parse(raw) as PackageGenerateResponse
  } catch {
    localStorage.removeItem(RECENT_PACKAGE_KEY)
    return null
  }
}

export function clearRecentPackage() {
  localStorage.removeItem(RECENT_PACKAGE_KEY)
}
