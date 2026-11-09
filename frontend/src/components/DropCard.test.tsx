import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router'
import { describe, expect, it } from 'vitest'
import type { Drop } from '../api'
import { makeDrop } from '../test/fixtures'
import { DropCard } from './DropCard'

function renderCard(drop: Drop) {
  // The card contains a link: it needs a router.
  return render(
    <MemoryRouter>
      <DropCard drop={drop} />
    </MemoryRouter>,
  )
}

describe('DropCard', () => {
  it('shows the product, linked to its detail page', () => {
    renderCard(makeDrop({ id: 3, product: 'Jordan 4 « Mayenne »' }))
    expect(screen.getByRole('link', { name: 'Jordan 4 « Mayenne »' })).toHaveAttribute(
      'href',
      '/drops/3',
    )
  })

  it('shows the price in euros', () => {
    renderCard(makeDrop({ price_cents: 18000 }))
    expect(screen.getByText(/^180,00\s€$/)).toBeInTheDocument()
  })

  it('shows the remaining stock', () => {
    renderCard(makeDrop({ remaining: 42, stock: 100 }))
    expect(screen.getByText('42 / 100 paires restantes')).toBeInTheDocument()
  })

  it.each([
    ['live', 'En vente'],
    ['upcoming', 'À venir'],
    ['sold_out', 'Épuisé'],
  ] as const)('shows the label of the %s status', (status, label) => {
    renderCard(makeDrop({ status, opens_at: '2100-01-01T00:00:00Z' }))
    expect(screen.getByText(label)).toBeInTheDocument()
  })
})
