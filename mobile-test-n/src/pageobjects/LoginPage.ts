```typescript
import { ChainablePromiseElement } from 'webdriverio';

class LoginPage {
    /**
     * Define selectors using getter methods
     */
    public get inputEmail(): ChainablePromiseElement<WebdriverIO.Element> {
        return $('~login-email-input');
    }

    public get inputPassword(): ChainablePromiseElement<WebdriverIO.Element> {
        return $('~login-password-input');
    }

    public get btnLogin(): ChainablePromiseElement<WebdriverIO.Element> {
        return $('~login-button');
    }

    public get errorMessage(): ChainablePromiseElement<WebdriverIO.Element> {
        return $('~login-error-message');
    }

    public get welcomeMessage(): ChainablePromiseElement<WebdriverIO.Element> {
        return $('~home-welcome-message');
    }

    /**
     * A method to open the app on the login screen
     * Assuming the app opens on login screen by default
     */
    public async open(): Promise<void> {
        // For mobile apps, usually no URL to open, but can reset app or launch app
        await driver.launchApp();
    }

    /**
     * Enter email address
     * @param email string
     */
    public async enterEmail(email: string): Promise<void> {
        const emailInput = await this.inputEmail;
        await emailInput.waitForDisplayed({ timeout: 5000 });
        await emailInput.setValue(email);
    }

    /**
     * Enter password
     * @param password string
     */
    public async enterPassword(password: string): Promise<void> {
        const passwordInput = await this.inputPassword;
        await passwordInput.waitForDisplayed({ timeout: 5000 });
        await passwordInput.setValue(password);
    }

    /**
     * Tap the login button
     */
    public async tapLogin(): Promise<void> {
        const loginBtn = await this.btnLogin;
        await loginBtn.waitForEnabled({ timeout: 5000 });
        await loginBtn.click();
    }

    /**
     * Check if login button is enabled
     */
    public async isLoginButtonEnabled(): Promise<boolean> {
        const loginBtn = await this.btnLogin;
        return loginBtn.isEnabled();
    }

    /**
     * Get error message text
     */
    public async getErrorMessage(): Promise<string> {
        const error = await this.errorMessage;
        await error.waitForDisplayed({ timeout: 5000 });
        return error.getText();
    }

    /**
     * Check if welcome message is displayed on home screen
     */
    public async isWelcomeMessageDisplayed(): Promise<boolean> {
        const welcome = await this.welcomeMessage;
        return welcome.isDisplayed();
    }
}

export default new LoginPage();
export { LoginPage };
```