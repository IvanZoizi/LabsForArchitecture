package labs2.views;

import java.util.List;

public interface View<T> {
    void updateData(List<T> data);
}
