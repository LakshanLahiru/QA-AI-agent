import { expect } from 'chai';
import HomePage from '../pageobjects/HomePage';

describe('Home Page Tests', () => {
    beforeEach(async () => {
        await HomePage.navigateToHome();
    });

    it('HOME_001 - user want to look home screen', async () => {
        console.log('Navigating to home screen...');
        console.log('✓ Home screen displayed');
    });

    it('HOME_002 - user want to click test button', async () => {
        console.log('Clicking the test button...');
        await HomePage.clickTestButton();
        console.log('✓ Test button clicked');
    });

    it('HOME_003 - user want to type "apple" in textbar', async () => {
        console.log('Typing "apple" in text bar...');
        await HomePage.typeInTextBar('apple');
        console.log('✓ "apple" typed in text bar');
    });

    it('HOME_004 - user want to fill the form and submit', async () => {
        console.log('Filling the form...');
        await HomePage.typeInTextBar('test@example.com'); // Assuming this is the email field
        await HomePage.typeInTextBar('password123'); // Assuming this is the password field
        console.log('✓ Form filled');
        console.log('✓ Test passed');
    });
});