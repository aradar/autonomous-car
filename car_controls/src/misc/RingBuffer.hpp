#ifndef __RINGBUFFER_CLASS__
#define __RINGBUFFER_CLASS__

#include <cstddef>
#include <algorithm>

template <typename T, size_t N>
class RingBuffer
{
	public:
		RingBuffer();
		T operator[](size_t index) const;
		void operator<<(const T& t);
		size_t size() const;

	private:
		size_t index_;
		T buffer_[N];
		size_t size_;
};


template <typename T, size_t N>
RingBuffer<T, N>::RingBuffer()
	: index_(0), size_(0)
{}

template <typename T, size_t N>
T RingBuffer<T, N>::operator[](size_t index) const
{
	//return buffer_[(index_+index) % N];
	return buffer_[index];
}

template <typename T, size_t N>
void RingBuffer<T, N>::operator<<(const T& t)
{
	size_ = std::min(size_+1, N);

	index_ = (index_ + 1) % N;
	buffer_[index_] = t;
}

template <typename T, size_t N>
size_t RingBuffer<T, N>::size() const
{
	return size_;
}

#endif
