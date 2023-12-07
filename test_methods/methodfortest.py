def rmall_filters(update, _):
    chat = update.effective_chat
    user = update.effective_user
    member = chat.get_member(user.id)
    if member.status != "creator" and user.id not in SUDO_USERS:
        update.effective_message.reply_text(
            "Only the chat owner can clear all notes at once."
        )
    else:
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Stop all filters", callback_data="filters_rmall"
                    )
                ],
                [InlineKeyboardButton(text="Cancel", callback_data="filters_cancel")]
            ]
        )
        update.effective_message.reply_text(
            f"Are you sure you would like to stop ALL filters in {chat.title}? This action cannot be undone.",
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN,
        )
