import { test, expect } from '@playwright/test';
import * as fs from 'fs';

type CSVRow = [string, string];


test('count table rows', async ({ page }) => {
  await page.goto('https://supportportal.juniper.net/s/article/Junos-Software-Versions-Suggested-Releases-to-Consider-and-Evaluate?language=en_US');

  const ACXseries = page.locator('table[summary="EX Series Ethernet Switches"]');
  const body = ACXseries.locator('tbody');
  const rows = body.locator('tr');
  const rowCount = await rows.count();
  console.log(rowCount);

  const csvRows: CSVRow[] = [];
  csvRows.push(["Device Name","Version Number"]); // Add headers to CSV

  for (let i = 0; i < rowCount; i++)
  {
      const row = rows.nth(i);

      const platform = await row.locator('td').nth(0).textContent();
      const version = await row.locator('td').nth(1).textContent();
      console.log(platform);
      console.log(version);
      csvRows.push([platform, version]);

  }
  const csvContent = csvRows.join('\n');
  const path = 'C:\Users\natef\OneDrive\Desktop\Projects\Customer Upgrade'
  fs.writeFileSync('Junyper_results.csv', csvContent, 'utf-8');
  
  console.log('Results written to Juniper_results.csv')
  
});