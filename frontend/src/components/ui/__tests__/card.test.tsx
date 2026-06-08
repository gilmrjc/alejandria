import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../card';

describe('Card components', () => {
  it('debe renderizar Card', () => {
    render(<Card>Test Card</Card>);
    expect(screen.getByText('Test Card')).toBeInTheDocument();
  });

  it('debe renderizar CardHeader', () => {
    render(<CardHeader>Test Header</CardHeader>);
    expect(screen.getByText('Test Header')).toBeInTheDocument();
  });

  it('debe renderizar CardTitle', () => {
    render(<CardTitle>Test Title</CardTitle>);
    expect(screen.getByText('Test Title')).toBeInTheDocument();
  });

  it('debe renderizar CardDescription', () => {
    render(<CardDescription>Test Description</CardDescription>);
    expect(screen.getByText('Test Description')).toBeInTheDocument();
  });

  it('debe renderizar CardContent', () => {
    render(<CardContent>Test Content</CardContent>);
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  it('debe renderizar CardFooter', () => {
    render(<CardFooter>Test Footer</CardFooter>);
    expect(screen.getByText('Test Footer')).toBeInTheDocument();
  });

  it('debe renderizar Card con className personalizado', () => {
    const { container } = render(<Card className="custom-class">Test</Card>);
    expect(container.firstChild).toHaveClass('custom-class');
  });
});
