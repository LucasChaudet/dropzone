import { expect, test, type APIRequestContext } from '@playwright/test'

// Each test creates its own drop through the API (behind nginx, under /api),
// so it never depends on the demo data or on another test.
async function createDrop(request: APIRequestContext, stock: number) {
  const response = await request.post('/api/drops', {
    data: {
      product: `E2E ${test.info().title} ${Date.now()}`,
      price_cents: 15000,
      stock,
      opens_at: '2000-01-01T00:00:00Z',
    },
  })
  expect(response.status()).toBe(201)
  return (await response.json()) as { id: number }
}

test('commander décrémente le stock', async ({ page, request }) => {
  const drop = await createDrop(request, 3)

  await page.goto(`/drops/${drop.id}`)
  await expect(page.getByTestId('remaining')).toHaveText('3 / 3 paires restantes')

  await page.getByRole('button', { name: 'Commander' }).click()

  await expect(page.getByRole('status')).toContainText('confirmée')
  await expect(page.getByTestId('remaining')).toHaveText('2 / 3 paires restantes')
})

test('un drop épuisé désactive le bouton', async ({ page, request }) => {
  const drop = await createDrop(request, 1)
  expect((await request.post(`/api/drops/${drop.id}/orders`)).status()).toBe(201)

  await page.goto(`/drops/${drop.id}`)

  await expect(page.getByTestId('remaining')).toHaveText('0 / 1 paires restantes')
  await expect(page.getByRole('button', { name: 'Épuisé' })).toBeDisabled()
})
