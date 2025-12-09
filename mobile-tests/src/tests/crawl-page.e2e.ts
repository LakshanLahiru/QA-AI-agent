/**
 * Crawling spec:
 * - Called by the backend /crawl-page endpoint.
 * - Uses CRAWL_PAGE_NAME env var to name the output file.
 * - Dumps driver.getPageSource() into ./crawls/{page}.xml
 */

import fs from 'node:fs';
import path from 'node:path';

describe('Crawl current page elements', () => {
    it('should dump page source to XML file', async () => {
        const pageName = process.env.CRAWL_PAGE_NAME || 'unknown';
        
        // Navigate to specific page if requested
        if (pageName.toLowerCase() === 'login') {
            try {
                console.log('Waiting for app to load...');
                // Wait for app to load
                await driver.pause(3000);
                
                console.log('Looking for Login navigation button...');
                // Click Login button in bottom navigation
                const loginNavButton = await $('~Login');
                await loginNavButton.waitForDisplayed({ timeout: 15000 });
                console.log('Found Login button, clicking...');
                await loginNavButton.click();
                
                // Wait for login screen to load
                console.log('Waiting for Login screen to load...');
                await driver.pause(3000);
                
                // Verify we're on login screen by checking for login elements
                try {
                    const emailInput = await $('~input-email');
                    await emailInput.waitForDisplayed({ timeout: 5000 });
                    console.log('✓ Successfully navigated to Login screen');
                } catch (verifyError) {
                    console.log('⚠ Could not verify login screen, but continuing...');
                }
            } catch (error) {
                console.log(`⚠ Could not auto-navigate to Login: ${error}`);
                console.log('Using current screen for crawl...');
            }
        } else if (pageName.toLowerCase() === 'forms') {
            try {
                await driver.pause(2000);
                const formsNavButton = await $('~Forms');
                await formsNavButton.waitForDisplayed({ timeout: 10000 });
                await formsNavButton.click();
                await driver.pause(2000);
                console.log('Navigated to Forms screen');
            } catch (error) {
                console.log('Could not auto-navigate to Forms, using current screen');
            }
        } else if (pageName.toLowerCase() === 'signup') {
            try {
                console.log('Waiting for app to load...');
                await driver.pause(3000);
                
                // First navigate to Login screen
                console.log('Navigating to Login screen...');
                const loginNavButton = await $('~Login');
                await loginNavButton.waitForDisplayed({ timeout: 15000 });
                await loginNavButton.click();
                await driver.pause(2000);
                
                // Then click Sign up button/tab
                console.log('Looking for Sign up button...');
                const signupButton = await $('~button-sign-up-container');
                await signupButton.waitForDisplayed({ timeout: 10000 });
                console.log('Clicking Sign up button...');
                await signupButton.click();
                
                // Wait for signup view to load
                await driver.pause(2000);
                console.log('✓ Successfully navigated to Sign up view');
            } catch (error) {
                console.log(`⚠ Could not auto-navigate to Sign up: ${error}`);
                console.log('Using current screen for crawl...');
            }
        } else if (pageName.toLowerCase() === 'swipe') {
            try {
                await driver.pause(2000);
                const swipeNavButton = await $('~Swipe');
                await swipeNavButton.waitForDisplayed({ timeout: 10000 });
                await swipeNavButton.click();
                await driver.pause(2000);
                console.log('Navigated to Swipe screen');
            } catch (error) {
                console.log('Could not auto-navigate to Swipe, using current screen');
            }
        } else if (pageName.toLowerCase() === 'text' || pageName.toLowerCase() === 'textinput') {
            try {
                console.log('Navigating to Text Input screen...');
                await driver.pause(2000);
                // Click Text Button to go to text input screen
                const textButton = await $('~Text Button');
                await textButton.waitForDisplayed({ timeout: 10000 });
                await textButton.click();
                await driver.pause(2000);
                console.log('✓ Successfully navigated to Text Input screen');
            } catch (error) {
                console.log(`⚠ Could not auto-navigate to Text Input: ${error}`);
                console.log('Using current screen for crawl...');
            }
        } else {
            // For other pages, wait a bit for user to navigate manually
            await driver.pause(3000);
        }
        
        const xml = await driver.getPageSource();

        // Save XML to crawls directory
        // Use process.cwd() which works from the WebDriverIO run context
        const crawlsDir = path.join(process.cwd(), 'crawls');
        if (!fs.existsSync(crawlsDir)) {
            fs.mkdirSync(crawlsDir, { recursive: true });
        }

        const outPath = path.join(crawlsDir, `${pageName}.xml`);
        fs.writeFileSync(outPath, xml, { encoding: 'utf-8' });
        console.log(`Crawl saved to: ${outPath}`);
    });
});


