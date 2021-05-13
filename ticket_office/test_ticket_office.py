def test_reserve():
    assert False

# SINGLE COACH, NO RESERVATION
# one seat
# __________ +1
# x_________
# multiple seats
# __________ +3
# xxx_______
# can reserve coach max capacity
# __________ +7
# xxxxxxx___
# cannot reserve above coach max capacity
# __________ +8
# __________
# SINGLE COACH, WITH RESERVATIONS
# one seat
# z_________ +1
# zx________
# multiple seats
# _z________ +3
# xzxx______
# can reserve up to coach max capacity
# zzzz_z____ +2
# zzzzxzx___
# cannot reserve above coach max capacity
# zzzzzz____ +2
# zzzzzz____
# MULTIPLE COACHES, NO RESERVATIONS
# can reserve in first coach
# _____ __________ +3
# xxx___ __________
# reserve in next coach if coach capacity is reached
# _____ __________ +7
# _____ xxxxxxx____
# can override coach max capacity
# __________ __________ +10
# xxxxxxxxxx __________
# cannot split a single reservation
# __________ __________ +11
# __________ __________
# MULTIPLE COACHES, WITH RESERVATIONS
# reserve in next coach if coach capacity is reached
# zzzzzz____ __________ +2
# zzzzzz____ xx________
# can override coach capacity
# zzzzzz____ zzzzzz____ +2
# zzzzzzxx__ zzzzzz____
# cannot reserve above train max capacity
# zzzzzzzz__ zzzzzz____ +1
# zzzzzzzz__ zzzzzz____
