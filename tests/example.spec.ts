import { test, expect } from '@playwright/test';
import * as fs from 'fs';

type CSVRow = [string, string];


test('count table rows', async ({ page }) => {
  await page.goto('https://community.fortinet.com/t5/FortiGate/Technical-Tip-Recommended-Release-for-FortiOS/ta-p/227178');

  // Wait for the pop-up to appear
  const popup = page.locator('div.engagement-popup');
  if (await popup.isHidden()) {
    console.log('Pop-up is initially hidden.');
  }
  await page.waitForSelector('div.engagement-popup', { state: 'attached', timeout: 5000 });
  // Interact with the pop-up (if it has a close button or content)
  const button = popup.locator('span.continue-as-guest');
  await button.click();


  // 
  // Locate the specific container
  const liaContent = page.locator('div.lia-message-body-content');

  // Locate the table within the container
  const outer_table = liaContent.locator('table');
  const target_row = outer_table.locator('tr').nth(2)
  const inner_table = target_row.locator('tbody');
  const rows = inner_table.locator('tr');
  const rowCount = await rows.count();
  console.log(rowCount);

  const csvRows: CSVRow[] = [];
  csvRows.push(["Device Name","Version Number"]); // Add headers to CSV

  for (let i = 1; i < rowCount; i++)
  {
    const row = rows.nth(i);

    
    const col1 = await row.locator('td').nth(0).textContent() || ' ';
    const col2 = await row.locator('td').nth(1).textContent() || ' ';
    const isVersion = /^\d+(\.\d+)*$/.test(col2);
    console.log(isVersion)

    // Initialize variables
    let deviceName: string;
    let versionNumber: string;

    if (isVersion == true)
    {
      deviceName = col1.trim();
      versionNumber = col2.trim();
    }
    else
    {
      deviceName = col2.trim();
      versionNumber = (await row.locator('td').nth(2).textContent())?.trim() || ' ';
    }


    console.log(deviceName);
    console.log(versionNumber);
    csvRows.push([deviceName, versionNumber]);
  }
  const csvContent = csvRows.join('\n');
  const path = 'C:\Users\natef\OneDrive\Desktop\Projects\Customer Upgrade'
  fs.writeFileSync('results.csv', csvContent, 'utf-8');

  console.log('Results written to results.csv')

  
});