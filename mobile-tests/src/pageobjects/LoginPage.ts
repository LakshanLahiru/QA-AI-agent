class LoginPage {
        public async navigateToLogin(): Promise<void> {
        await driver.pause(2000); // Wait for app to load
    // Dismiss any alerts/popups first
    try { const okBtn = await $('android=new UiSelector().text("OK")'); if (await okBtn.isDisplayed()) { await okBtn.click(); await driver.pause(1000); } } catch (e) { /* No alert */ }
    try { const okBtn2 = await $('~OK'); if (await okBtn2.isDisplayed()) { await okBtn2.click(); await driver.pause(1000); } } catch (e) { /* No alert */ }
    // Reset to home screen first for consistent state
    try {
        const homeNav = await $('~Home');
        await homeNav.waitForDisplayed({ timeout: 5000 });
        await homeNav.click();
        await driver.pause(2000);
    } catch (e) {
        // Home button not found, continue anyway
    }
    // Check if already on login screen
    try {
        const emailInput = await $('~input-email');
        await emailInput.waitForDisplayed({ timeout: 2000 });
        console.log('Already on login screen');
        return; // Already on target screen
    } catch (e) {
        // Not on login screen, navigate to it
        const nav = await $('~Login');
        await nav.waitForDisplayed({ timeout: 10000 });
        await nav.click();
        await driver.pause(2000);
        // Verify we're on login screen
        const emailInput = await $('~input-email');
        await emailInput.waitForDisplayed({ timeout: 10000 });
    }
    }


    public get input_email() { return $('~input-email'); }
    public get input_password() { return $('~input-password'); }
    public get button_login() { return $('~button-LOGIN'); }
    public get button_sign_up() { return $('~button-sign-up-container'); }

    public async enterEmail(email: string): Promise<void> {
        const el = await this.input_email;
        await el.waitForDisplayed({ timeout: 5000 });
        await el.setValue(email);
    }

    public async enterPassword(password: string): Promise<void> {
        const el = await this.input_password;
        await el.waitForDisplayed({ timeout: 5000 });
        await el.setValue(password);
    }

    public async clickLoginButton(): Promise<void> {
        const el = await this.button_login;
        await el.waitForDisplayed({ timeout: 5000 });
        await el.click();
    }
}

export default new LoginPage();
export { LoginPage };