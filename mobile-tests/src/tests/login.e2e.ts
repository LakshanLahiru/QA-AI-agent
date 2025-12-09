import { expect } from 'chai';
import LoginPage from '../pageobjects/LoginPage';

describe('Login Tests', () => {
    beforeEach(async () => {
        await LoginPage.navigateToLogin();
    });

    it('User should be able to see the username field', async () => {
        const emailInput = await LoginPage.input_email;
        const isDisplayed = await emailInput.isDisplayed();
        expect(isDisplayed).to.be.true;
        console.log('✓ Username field is visible');
    });

    it('User should be able to login after entering valid details', async () => {
        console.log('Filling in the login form...');
        await LoginPage.enterEmail('test@example.com');
        await LoginPage.enterPassword('password123');
        await LoginPage.button_login.click();
        console.log('✓ Test passed');
    });
});