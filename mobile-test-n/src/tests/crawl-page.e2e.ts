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
        const xml = await driver.getPageSource();

        const crawlsDir = path.resolve(__dirname, '..', '..', 'crawls');
        if (!fs.existsSync(crawlsDir)) {
            fs.mkdirSync(crawlsDir, { recursive: true });
        }

        const outPath = path.join(crawlsDir, `${pageName}.xml`);
        fs.writeFileSync(outPath, xml, { encoding: 'utf-8' });
        console.log(`Crawl saved to: ${outPath}`);
    });
});


