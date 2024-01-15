import React from "react";
import { render, screen } from "@testing-library/react";
import axios from "axios";
import ActorsPage from "../pages/ActorsPage";

jest.mock("axios");

describe("ActorsPage", () => {
  test("renders loading text initially", () => {
    render(<ActorsPage />);
    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  test("renders fetched data", async () => {
    const mockData = [
      { id: 1, name: "Item 1", avatar: "https://dummyimage.com/125x125/caf4fa/" },
      { id: 2, name: "Item 2", avatar: "https://dummyimage.com/125x125/caf4fa/" },
    ];
    axios.get.mockResolvedValueOnce({ data: mockData });

    render(<ActorsPage />);
    expect(await screen.findByText("Item 1")).toBeInTheDocument();
    expect(await screen.findByText("Item 2")).toBeInTheDocument();
  });

  test("handles API error", async () => {
    const errorMessage = "API error";
    axios.get.mockRejectedValueOnce(new Error(errorMessage));

    render(<ActorsPage />);
    expect(await screen.findByText("Loading...")).toBeInTheDocument();
    expect(await screen.findByText(errorMessage)).toBeInTheDocument();
  });
});