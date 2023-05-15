import type { PlaywrightTestConfig } from '@playwright/test'
import { getBaseUrl } from './helpers/urls'
import { devices } from '@playwright/test'

const config: PlaywrightTestConfig = {
    timeout: 5 * 60 * 1000,
    expect: {
        timeout: 5000,
    },
    retries: process.env.CI ? 1 : 0,
    workers: process.env.CI ? 5 : 1,
    reporter: [['html', { open: 'always'}], ['list'], ['allure-playwright', {
        detail: true,
        suiteTitle: false
    }]],
    use: {
        viewport: { width: 1280, height: 720 },
        headless: true,
        trace: 'on',
        screenshot: 'on',
        video: 'off',
        ignoreHTTPSErrors: true,
        baseURL: getBaseUrl(),
    },

    projects: [
        {
            name: 'chrome',
            use: {
                channel: 'chrome',
            },
        }
    ],

    outputDir: 'test-results/',
}

export default config
