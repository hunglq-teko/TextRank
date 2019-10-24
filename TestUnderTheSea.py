import underthesea 
from underthesea import word_tokenize, pos_tag 

print(pos_tag('''Nữ trưởng phòng dùng bằng cấp của chị bị thôi việc
Bà Trần Thị Ngọc Thêm, Trưởng phòng Quản trị - Văn phòng Tỉnh ủy Đăk Lăk, bị khai trừ Đảng, buộc thôi việc vì dùng bằng cấp 3 của chị ruột.

Ngoài ra, Uỷ ban Kiểm tra Tỉnh ủy Đăk Lăk cũng đang xác minh nguyên nhân dẫn đến sai phạm của bà Thêm (44 tuổi) và xem xét trách nhiệm của 6 cán bộ liên quan, ông Nguyễn Thượng Hải, Chánh văn phòng Tỉnh ủy Đăk Lăk cho biết, chiều 23/10.

16 năm trước, bà Thêm (quê Lâm Đồng, tên thường gọi Trần Thị Ngọc Thảo) sử dụng bằng THPT của chị ruột tên Trần Thị Ngọc Ái Sa để vào làm nhân viên hợp đồng tại Nhà khách Tỉnh ủy Đăk Lăk. 

Ít năm sau, bà được kết nạp Đảng rồi chuyển sang Văn phòng Tỉnh ủy làm việc. Năm 2013 bà Thêm được bổ nhiệm phó phòng quản trị, năm 2016 làm trưởng phòng.

Khi bị bại lộ, bà Thêm cho rằng, lúc đó còn trẻ, suy nghĩ chưa chín chắn và nông nổi. Chỉ muốn có việc làm để mưu sinh trong lúc gia đình đang khó khăn nên đã lấy tên chị ruột. Nữ trưởng phòng thừa nhận việc làm của mình là sai.

Chiều cùng ngày, bà Bùi Thị Thân, Phó phòng Hành chính (Văn phòng Tỉnh ủy Đăk Lăk) cũng bị kỷ luật khiển trách và cách chức xuống làm nhân viên Phòng Hành chính, vì dùng bằng cấp 3 giả để tiến thân.'''))