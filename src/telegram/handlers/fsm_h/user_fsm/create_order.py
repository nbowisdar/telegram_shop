


# @user_router.callback_query(Text(startswith="new_order_g"))
# async def anon(callback: CallbackQuery, state: FSMContext):
#     prefix, category = callback.data.split('|')
#     await state.update_data(category=category)
#     await callback.message.edit_text("Оберіть товар",
#                                      reply_markup=build_goods_with_price_inl(category))

