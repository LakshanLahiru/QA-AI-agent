```typescript
import LoginPage from '../pageobjects/LoginPage';
import { expect } from 'chai';

describe('Login Feature', () => {
    const loginPage = new LoginPage();

    beforeEach(async () => {
        await loginPage.open();
    });

    it('LOGIN_001 - User can log in with valid email and password and land on the home screen', async () => {
        await loginPage.setEmail('validuser@example.com');
        await loginPage.setPassword('validPassword123');
        await loginPage.tapLoginButton();

        const homeScreenWelcome = await loginPage.getHomeScreenWelcomeMessage();
        expect(homeScreenWelcome).to.exist;
        expect(homeScreenWelcome).to.contain('Welcome');
    });

    it('LOGIN_002 - User sees an error when logging in with an invalid password', async () => {
        await loginPage.setEmail('validuser@example.com');
        await loginPage.setPassword('invalidPassword');
        await loginPage.tapLoginButton();

        const errorMessage = await loginPage.getLoginErrorMessage();
        expect(errorMessage).to.exist;
        expect(errorMessage).to.contain('error');
        expect(await loginPage.isOnLoginScreen()).to.be.true;
    });

    it('LOGIN_003 - Login button is disabled until both fields are filled', async () => {
        // Initially both fields blank
        expect(await loginPage.isLoginButtonEnabled()).to.be.false;

        // Fill only email
        await loginPage.setEmail('validuser@example.com');
        expect(await loginPage.isLoginButtonEnabled()).to.be.false;

        // Clear email, fill only password
        await loginPage.setEmail('');
        await loginPage.setPassword('somePassword');
        expect(await loginPage.isLoginButtonEnabled()).to.be.false;

        // Fill both fields
        await loginPage.setEmail('validuser@example.com');
        expect(await loginPage.isLoginButtonEnabled()).to.be.true;
    });
});
```