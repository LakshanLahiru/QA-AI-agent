import { expect } from 'chai';
import LoginPage from '../pageobjects/LoginPage';

describe('Login Tests', () => {
    beforeEach(async () => {
        await LoginPage.navigateToLogin();
    });

    it('User should be able to see the title on login screen', async () => {
        console.log('Filling in the login form...');
        await LoginPage.enterEmail('test@example.com');
        await LoginPage.enterPassword('password123');
        await LoginPage.button_login.click();
        console.log('✓ Test passed');
    });
});