"""
This module contains tools for managing Trello cards.
"""

import logging
from typing import List, Optional
from datetime import datetime

from mcp.server.fastmcp import Context

from server.models import TrelloCard
from server.services.card import CardService
from server.trello import client
from server.dtos.update_card import UpdateCardPayload
from server.mcp_instance import mcp

logger = logging.getLogger(__name__)

service = CardService(client)


@mcp.tool()
async def get_card(context: Context, card_id: str) -> TrelloCard:
    """Retrieves a specific card by its ID.

    Args:
        card_id (str): The ID of the card to retrieve.

    Returns:
        TrelloCard: The card object containing card details.
    """
    try:
        logger.info(f"Getting card with ID: {card_id}")
        result = await service.get_card(card_id)
        logger.info(f"Successfully retrieved card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get card: {str(e)}"
        logger.error(error_msg)
        await context.error(error_msg)
        raise


@mcp.tool()
async def get_cards(context: Context, list_id: str, from_date: Optional[str] = None) -> List[TrelloCard]:
    """Retrieves all cards in a given list, optionally filtered by creation or last activity date.

    Args:
        list_id (str): The ID of the list whose cards to retrieve.
        from_date (str, optional): ISO 8601 date string. Only cards created or updated on/after this date are returned.

    Returns:
        List[TrelloCard]: A list of card objects.
    """
    try:
        logger.info(f"Getting cards for list: {list_id}")
        result = await service.get_cards(list_id)
        logger.info(f"Successfully retrieved {len(result)} cards for list: {list_id}")
        if from_date:
            try:
                cutoff = datetime.fromisoformat(from_date)
            except Exception:
                await context.error(f"Invalid from_date format: {from_date}. Use ISO 8601 format.")
                return []
            filtered = []
            for card in result:
                created = card.creationDate
                updated = card.dateLastActivity
                if (created and created >= cutoff) or (updated and updated >= cutoff):
                    filtered.append(card)
            return filtered
        return result
    except Exception as e:
        error_msg = f"Failed to get cards: {str(e)}"
        logger.error(error_msg)
        await context.error(error_msg)
        raise


@mcp.tool()
async def create_card(
    context: Context, list_id: str, name: str, desc: str | None = None
) -> TrelloCard:
    """Creates a new card in a given list.

    Args:
        list_id (str): The ID of the list to create the card in.
        name (str): The name of the new card.
        desc (str, optional): The description of the new card. Defaults to None.

    Returns:
        TrelloCard: The newly created card object.
    """
    try:
        logger.info(f"Creating card in list {list_id} with name: {name}")
        result = await service.create_card(list_id, name, desc)
        logger.info(f"Successfully created card in list: {list_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to create card: {str(e)}"
        logger.error(error_msg)
        await context.error(error_msg)
        raise


@mcp.tool()
async def update_card(
    context: Context, card_id: str, payload: UpdateCardPayload
) -> TrelloCard:
    """Updates a card's attributes.

    Args:
        card_id (str): The ID of the card to update.
        **kwargs: Keyword arguments representing the attributes to update on the card.

    Returns:
        TrelloCard: The updated card object.
    """
    try:
        logger.info(f"Updating card: {card_id} with payload: {payload}")
        result = await service.update_card(
            card_id, **payload.model_dump(exclude_unset=True)
        )
        logger.info(f"Successfully updated card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to update card: {str(e)}"
        logger.error(error_msg)
        await context.error(error_msg)
        raise


@mcp.tool()
async def delete_card(context: Context, card_id: str) -> dict:
    """Deletes a card.

    Args:
        card_id (str): The ID of the card to delete.

    Returns:
        dict: The response from the delete operation.
    """
    try:
        logger.info(f"Deleting card: {card_id}")
        result = await service.delete_card(card_id)
        logger.info(f"Successfully deleted card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to delete card: {str(e)}"
        logger.error(error_msg)
        await context.error(error_msg)
        raise


@mcp.tool()
async def move_card(context: Context, card_id: str, target_list_id: str) -> TrelloCard:
    """
    Moves a card to a different list (column) by updating its idList.

    Args:
        card_id (str): The ID of the card to move.
        target_list_id (str): The ID of the target list (column).

    Returns:
        TrelloCard: The updated card object after moving.
    """
    try:
        logger.info(f"Moving card {card_id} to list {target_list_id}")
        result = await service.update_card(card_id, idList=target_list_id)
        logger.info(f"Successfully moved card {card_id} to list {target_list_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to move card: {str(e)}"
        logger.error(error_msg)
        await context.error(error_msg)
        raise
