class Home {
        public async navigateToHome(): Promise<void> {
        await driver.pause(2000); // Wait for app to load
    // Dismiss any alerts/popups first
    try { const okBtn = await $('android=new UiSelector().text("OK")'); if (await okBtn.isDisplayed()) { await okBtn.click(); await driver.pause(1000); } } catch (e) { /* No alert */ }
    try { const okBtn2 = await $('~OK'); if (await okBtn2.isDisplayed()) { await okBtn2.click(); await driver.pause(1000); } } catch (e) { /* No alert */ }
    }


    public get testButton() {
        return $('~Test Button');
    }

    public get textBar() {
        return $('~Text Bar');
    }

    public async clickTestButton() {
        const btn = await this.testButton;
        await btn.waitForDisplayed({ timeout: 5000 });
        await btn.click();
    }

    public async typeInTextBar(value: string) {
        const input = await this.textBar;
        await input.waitForDisplayed({ timeout: 5000 });
        await input.setValue(value);
    }
}

export default new Home();
export { Home };